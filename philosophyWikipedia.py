from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import networkx as nx

def output(canPhilosophyBeReached, listPagesVisited):
    """Outputs whether a certain page reached the Philosophy Wikipedia page and how many pages you had to visit to reach Philosophy

    Args:
        canPhilosophyBeReached (boolean): Booleans that states whether Philosophy was reached
        listPagesVisited (list): List with the names of the Wikipedia Pages you visited
    """
    
    if not canPhilosophyBeReached:      # Philosophy can't be reached
        print(f"You found an exception! The wikipedia page of {listPagesVisited[0]} does not go to Philosophy")
        print()
    else:                               # Philosophy can be reached
        print(f'You have to visit {len(listPagesVisited)} pages and click {len(listPagesVisited)-1} links to get to the Philosophy Wikipedia page from the {listPagesVisited[0]} Wikipedia page.')

def filterLinks(elementToSearch):
    """Given an element, this functions searches for all valid links according to the rules of the Philosophy Wikipedia Game inside a specific element and returns a list of all valid links.

    Args:
        elementToSearch (bs4.element.Tag): An html element (usually a paragraph element (<p>) or a list element (<li>) )

    Returns:
        list: A list that contains all the valid links one could click inside that element.
    """

    linkList = []
    
    # Validates that the element isn't empty
    if elementToSearch.text != "\n":
        initialListOfLinks = []   # Stores links that are not within parenthesis
        parenthesisCount = 0
        
        # Finds all links in elementToSearch that are not contained within parenthesis
        for element in elementToSearch.descendants:
            if isinstance(element, str):
                for char in element:
                    if char == "(":
                        parenthesisCount += 1
                    elif char == ")":
                        parenthesisCount -=1
            elif element.name == 'a' and parenthesisCount == 0 and ('href' in element.attrs):
                initialListOfLinks.append(element)
        
        # Find all links that are citations in elementToSearch
        linkListCitations = [element.find('a') for element in elementToSearch.find_all('sup')]
        
        # Removes all links that are citations from our initial list of links
        linkListWOCitations = [link for link in initialListOfLinks if link not in linkListCitations]
        linkList = linkListWOCitations[:]
    return linkList

def extractElements(soup):
    """Returns a list of html elements that we know could contain links that we can "click" on. This function helps us exclude elements that could potentially have links that we cannot "click" on.

    Args:
        soup (BeautifulSoup): All the html contents of the wikipedia file
        
    Returns:
        list: A list that contains all valid paragraph and list elements in a wikipedia page that contains a link we can click according to our constraints.
    """
    # Finding all <p> and <li> elements in our wikipedia page
    correctDiv = soup.find(id='mw-content-text')
    totalElements = correctDiv.find_all(['p', 'li'])
    
    # Finding specific <p> and <li> elements that contain links we CANNOT click on
    selectors = ['table p', 'table li', 'div.navbar li', 'div.thumbcaption li']
    elementsInTable = []
    for selector in selectors:
        elementsInTable += correctDiv.select(selector)
    
    # Removing html elements that contain links we cannot click on
    correctElements = [element for element in totalElements if element not in elementsInTable]
    return correctElements

def validateURL(url):
    """Makes sure that the url the user inputs is a wikipedia url"""
    if not url.startswith("https://en.wikipedia.org"):
        raise ValueError

def getFirstValidURL(url):
    """Given a Wikipedia URL, this function finds the first valid url that we can click based on the rules of the Philosophy Game. This function will return an empty string if there is no valid link we can click.

    Args:
        url (string): A url of a wikipedia page

    Returns:
        string: Returns the url of the next valid url we can "click" on based on the rules of the Philosophy Game
    """
    # Getting elements from url that could contain a valid url that we can click
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')
    elements = extractElements(soup)
    
    # Going through each element that could have a valid url. 
    # When we find an element that has a list of valid urls, we return the first url in that list and end the process (we only need one valid link)
    for element in elements:
        linkList = filterLinks(element)
        if linkList:
            return "https://en.wikipedia.org" + linkList[0]['href']
    return ""

def philosophyGame(url):
    """Given a wikipedia url, this function finds out whether is it possible to reach the Philosophy Wikipedia Page from the initial url by clicking the first link of each wikipedia page we go to.

    Args:
        url (string): A wikipedia url

    Returns:
        tuple(boolean, list): A tuple with two elements. The first element contains a boolean on if it is possible for the initial url given to reach the Philosophy Wikipedia page. The second element is a list of the Wikipedia page names that were visited in an attempt to reach Philosophy.
    """
    
    # Using a set to track the urls visited as it saves some computation time
    urlTracker = set()
    try:
        # Makes sure that url is a wikipedia url
        validateURL(url)
        pagesVisited = [url.split("/")[-1]]
        isPhilosophyPossible = True
        
        # Iterates through each wikipedia page and finds the next link in each page
        while url != 'https://en.wikipedia.org/wiki/Philosophy':
            
            # Validates that we haven't gone in a loop when accessing urls
            if url in urlTracker:
                isPhilosophyPossible = False
                break
            
            urlTracker.add(url)
            
            # Gets the first link that appears in url
            url = getFirstValidURL(url)
            
            
            # If url == "", it means that there are no valid urls we can click on the current wikipedia page. 
            # Since we for sure aren't at the philosophy page, it means that it is impossible for us to get to the philosophy page.
            if url == "":
                isPhilosophyPossible = False
                break
            


            pagesVisited.append(url.split("/")[-1])

        return isPhilosophyPossible, pagesVisited
            
    # Handles exceptions related to bad input (input is not a wikipedia url)
    except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
        print("ERROR: The URL is invalid or uses an unsupported schema.")
    except ValueError:
        print("ERROR: A non wikipedia url was inputted. Please try again.")

def addNodesToGraph(listOfPagesVisited, G):
    """Given a list of the pagesVisited, this function adds this path to graph G

    Args:
        listOfPagesVisited (list): List of the Wikipedia Page names which shows the path you have to take from a random Wikipedia Page to reach the Philosophy Wikipedia Page
        G (class Graph): A graph object that will contain the path taken
    """
    edgeList = []
    for i in range(len(listOfPagesVisited)-1):
        edge = (listOfPagesVisited[i], listOfPagesVisited[i+1])
        edgeList.append(edge)
    G.add_edges_from(edgeList)
    
def printGraph(G):
    """This function intends to return a visual graphic of G so you can visualize the paths of certain Wikipedia webpages to philosophy.
    This function is work in progress as there is overlap in the nodes when printing this function.

    Args:
        G (Graph): The graph that you want to display
    """
    # Formats the final output of the Graph
    pos = nx.spring_layout(G, k=0.05, seed=40)
    plt.figure(figsize=(15,15), facecolor="#A9AAB1")
    nx.draw_networkx_edges(G, pos, edge_color='#011627', width=2.0)
    labels = {node: node for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color='k', bbox= dict(facecolor='#BE9D9E', edgecolor='black', boxstyle="round,pad=0.2"))
    # Highlights the Philosophy node in the graph to make it easier to see where it is
    if "Philosophy" in G.nodes():
        nx.draw_networkx_nodes(G, pos, nodelist=["Philosophy"], node_size= 600, node_color="#0A2463")
    
    plt.axis("off")
    plt.title("Path to Philosophy Map")
    plt.show()

def main():
    """An example of how you could use the functions above for the Philosophy Game
    """
    urlList = ['Pianist', 'Computer Science', 'President']
    G = nx.Graph()
    for name in urlList:
        url ="https://en.wikipedia.org/wiki/" + name
        philosophyPossible, listOfPagesVisited = philosophyGame(url)
        print(listOfPagesVisited)
        addNodesToGraph(listOfPagesVisited, G)
        
    printGraph(G)
    
if __name__ == "__main__":
    main()
