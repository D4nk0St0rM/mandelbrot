##### mandelbrot
A simple Python Mandelbrot function


The Mandelbrot set is an example of a fractal in mathematics. It is named after Benoît Mandelbrot, a Polish-French-American mathematician. 

The Mandelbrot set is important for chaos theory. The edging of the set shows a self-similarity, which is perfect, but because of the minute detail, it looks like it evens out.

The Mandelbrot set can be explained with the equation z<sub>n+1</sub> = z<sub>n</sub><sup>2</sup> + c. 

In that equation, c and z are complex numbers and n is zero or a positive integer (natural number). Starting with z<sub>0</sub> = 0, c is in the Mandelbrot set if the absolute value of zn never becomes larger than a certain number (that number depends on c), no matter how large n gets.

Mandelbrot was one of the first to use computer graphics to create and display fractal geometric images, leading to his discovering the Mandelbrot set in 1979. That was because he had access to IBM's computers. He was able to show how visual complexity can be created from simple rules. He said that things typically considered to be "rough", a "mess" or "chaotic", like clouds or shorelines, actually had a "degree of order". The equation z<sub>n+1</sub> = z<sub>n</sub><sup>2</sup> + c was known long before Benoit Mandelbrot used a computer to visualize it.

Images are created by applying the equation to each pixel in an iterative process, using the pixel's position in the image for the number 'c'. 'c' is obtained by mapping the position of the pixel in the image relative to the position of the point on the complex plane.

[source](https://simple.wikipedia.org/wiki/Mandelbrot_set)

