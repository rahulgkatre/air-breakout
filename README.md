# Air Breakout

HackGT 2019 project by Rahul Katre

### Inspiration

I am interested in computer vision so when I was messing around with color filtering in order to track an object, I realized that I can use it to control the movement of some object, like the mouse on my screen. It wasn't very accurate, so I decided to use it for something that only needs precision in one direction, like a paddle in Breakout.

### What it does

Using the laptop's webcam, the program tracks the highlighter in the frame of the camera, and uses it to move a paddle in Atari Breakout.

### How I built it

Using OpenCV, the pixels in the frame are filtered for colors that are close to the color of the highlighter, and the resulting pixels resemble a white blob. In order to track the object, the program finds just one of the pixels in the white blob and uses its position in the frame to figure out where the paddle should move (the resolution of the camera and the game is almost the same.

### Challenges I ran into

I had to run some denoising on the image so that I could track it better, and the game stuttered a lot so I also had to implement multithreading so that the game and the camera processing would run on two separate threads.

### Accomplishments that I'm proud of

This is the first time I successfully implemented OpenCV in a project, and this was also a project that I came up with without inspiration from other's projects or even my own past projects.

### What I learned

I learned how to better implement multithreading and communication between threads, and I also learned the basics of PyGame, which the game aspect of the program is written using.

### What's next for Air Breakout

Not Air Breakout, but 2 player Air Pong! Using 2 different colored highlighters (one for each player), each player can control a paddle to hit a ball between the paddles, without touching the computer at all.

### Built with

Multithreading, OpenCV and PyGame in Python
