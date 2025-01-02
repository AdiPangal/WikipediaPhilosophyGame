# Wikipedia Philosophy Game Introduction

If you open up a random Wikipedia Page, click the first link in the article body that isn't italicized or in parenthesis, and then repeat this process for each subsequent Wikipedia Page, you will reach the Philosophy Wikipedia Page around 97% of the time (you should try it!). This is what I call the Wikipedia Philosophy Game.

I felt that it would be cool to code this process given an initial wikipedia url, and this repository contains the code made to simulate the game. This was coded in Python and uses the BeautifulSoup library to help me extract the correct link from each Wikipedia Page. I also tried to make a couple of functions that allows you to create a graph structure to help you visualize the paths that Wikipedia Pages take to reach Philosophy. There are some issues with this function such as resulting in a graph with edges overlapping each other, leading to a cluttered graph. I hope to fix these eventually.

Though the main code that finds the correct link in each Wikipedia Page works, there are some improvements I still want to make.

# Future Improvements
1) If you have a list of links that you put into the philosophyGame function, it takes a really long time to run. I hope to optimize my code (specifically in the process of finding the first valid link) to reduce runtime.
2) Though I had a fun time using networkx, I believe that this isn't the best library to create graph structures to show the path of certain Wikipedia Pages to Philosophy. I had issues of paths overlapping each other and making weird curved paths making the graph difficult to understand. I hope to use the plotly library in the future to fullfill this function of making diagrams (Any other suggestions would be appreciated). 
