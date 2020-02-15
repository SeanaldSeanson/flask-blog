# Design Diary
[Application Walkthrough](walkthrough.gif)

One particular struggle I had to deal with was understanding the session system in Flask. I hadn't initially realized how simply adding a value to the session object as I would with a dictionary would cause so much other work to be done in the background, so it took some research for me to grasp that well enough to be fully comfortable using sessions.

Some of my biggest problems with this project related to the translation of the data the application handles into the web pages it displays. I felt relatively comfortable with writing the parts of the code that process the data in the background, but I'm not particularly well-versed in the web-specific parts of this kind of project, like HTML, CSS, or Javascript, which I think is a big part of why those parts of my code tennded to turn out rather ugly, and in retrospect I felt that I didn't make use of the tools that Flask provides for this, like templates, to as great an extent that I should have.

To a future student working on this assignment, I would recommend starting any research on a particular problem by referencing the official Python or Flask documentation on the function or feature in question. Even when referencing the documentation didn't immediately clear up my confusion, it made it easier to understand the solutions I did find elsewhere.

I'm a bit of an enthusiast about information security, so I particularly enjoyed implementing my own authentication system for the website. It wasn't a particularly hard part of the project, but I enjoyed applying my knowledge of what a proper modern authentication system looks like to a programming project (not to say mine necessarily meets such a standard).

One of the more challenging aspects of this assignment for me was trying to make up for my relative lack of web-specific knowledge. I managed to throw together what I needed for this project.

I thought the requirements of the assignment were communicated well. I didn't find anything particularly difficult to understand there.

I had the thought that it might be a good idea to make this (optionally) a group project, so that people could pair up who would complement each other's existing skillsets.
