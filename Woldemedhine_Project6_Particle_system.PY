"""
Name: Caleb woldemedhine
Purpose: This python file creats a particle sytem with fire
Course: COMP1352
Assignment: Project 6
Collaborators: 1352 Instructors
Internet Sources: None
"""

import dudraw   
import random  
import math 

# Vector Class: Defines operations for 2D vectors
class Vector:
    def __init__(self, some_x=0, some_y=0):  # Initializing a Vector object with default or given coordinates
        self.x = some_x  # Setting the x-coordinate
        self.y = some_y  # Setting the y-coordinate

    def limit(self, l):  # Limiting the magnitude of the vector
        if self.length() >= l:
            self.resize(l)

    def resize(self, l):  # Resizing the vector to a specified length
        length = math.sqrt(self.x ** 2 + self.y ** 2)  # Calculating the current length of the vector
        self.x *= (l / length)  # Adjusting the x-coordinate
        self.y *= (l / length)  # Adjusting the y-coordinate

    def __add__(self, other_vector):  # Defining addition operation for vectors
        return Vector(self.x + other_vector.x, self.y + other_vector.y)  # Adding two vectors

    def __sub__(self, other_vector):  # Defining subtraction operation for vectors
        return Vector(self.x - other_vector.x, self.y - other_vector.y)  # Subtracting two vectors

    def __isub__(self, other_vector):  # Defining in-place subtraction operation for vectors
        self.x -= other_vector.x
        self.y -= other_vector.y
        return self

    def __iadd__(self, other_vector):  # Defining in-place addition operation for vectors
        self.x += other_vector.x
        self.y += other_vector.y
        return self

    def divide(self, s):  # Dividing the vector by a scalar value
        self.x /= s
        self.y /= s

    def length(self):  # Calculating the length (magnitude) of the vector
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle_in_radians(self):  # Calculating the angle of the vector in radians
        return math.atan2(self.y, self.x)


# Time Class: Manages time in frames
class Time:
    frame = 0  # Initializing the frame count

    @staticmethod
    def tick():  # Function to increment the frame count
        Time.frame += 1

    @staticmethod
    def time():  # Function to get the current frame count
        return Time.frame


# Particle Class: Represents a generic particle
class Particle:
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):  # Initializing a particle object
        self.pos = Vector(x_pos, y_pos)  # Setting the position vector
        self.vel = Vector(x_vel, y_vel)  # Setting the velocity vector
        self.size = size  # Setting the size of the particle
        self.color = dudraw.Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))  # Setting a random color
        self.lifetime = lifetime  # Setting the lifetime of the particle

    def has_expired(self):  # Checking if the particle's lifetime has expired
        return self.lifetime <= 0

    def move(self):  # Moving the particle based on its velocity
        if not self.has_expired():  # If the particle has not expired
            self.pos += self.vel  # Update the position


# SparkParticle Class: Represents a spark particle
class SparkParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):  # Initializing a spark particle
        super().__init__(x_pos, y_pos, x_vel, y_vel, size, lifetime)  # Calling the parent class constructor
        self.color = dudraw.Color(213, 173, 73)  # Setting a specific color for spark particles

    def draw(self):  # Drawing the spark particle
        dudraw.set_pen_color(self.color)  # Setting the drawing color
        dudraw.line(self.pos.x, self.pos.y, self.pos.x + self.vel.x, self.pos.y + self.vel.y)  # Drawing a line indicating the spark's direction
        dudraw.line(self.pos.x, self.pos.y, self.pos.x - self.vel.x, self.pos.y - self.vel.y)  # Drawing another line for visual effect


# AcceleratingParticle Class: Represents a particle with acceleration
class AcceleratingParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, size, lifetime):  # Initializing an accelerating particle
        super().__init__(x_pos, y_pos, x_vel, y_vel, size, lifetime)  # Calling the parent class constructor
        self.acc = Vector(x_acc, y_acc)  # Setting the acceleration vector

    def move(self):  # Moving the particle with acceleration
        if not self.has_expired():  # If the particle has not expired
            self.vel += self.acc  # Update the velocity with acceleration
            self.pos += self.vel  # Update the position


# FireworkParticle Class: Represents a particle in a firework
class FireworkParticle(AcceleratingParticle):
    def draw(self):  # Drawing the firework particle
        dudraw.set_pen_color(self.color)  # Setting the drawing color
        dudraw.filled_square(self.pos.x, self.pos.y, self.size)  # Drawing a square for the firework particle


# FireParticle Class: Represents a particle in fire
class FireParticle(Particle):
    def __init__(self, x_pos, y_pos, x_vel, y_vel, size, lifetime):  # Initializing a fire particle
        super().__init__(x_pos, y_pos, x_vel, y_vel, size, lifetime)  # Calling the parent class constructor
        self.color = [213, 173, 73]  # Setting a specific color for fire particles

    def draw(self):  # Drawing the fire particle
        self.color[1] -= 3  # Modifying the color gradually
        dudraw.set_pen_color_rgb(self.color[0], self.color[1], self.color[2])  # Setting the drawing color
        dudraw.filled_circle(self.pos.x, self.pos.y, self.size)  # Drawing a filled circle for the fire particle

    def move(self):  # Moving the fire particle
        self.pos += self.vel  # Update the position
        self.size -= 0.0003  # Decrease the size gradually


# MarbleParticle Class: Represents a marble-like particle
class MarbleParticle(AcceleratingParticle):
    def draw(self):  # Drawing the marble particle
        dudraw.set_pen_color(self.color)  # Setting the drawing color
        dudraw.filled_circle(self.pos.x, self.pos.y, self.size)  # Drawing a filled circle for the marble particle

    def move(self):  # Moving the marble particle
        if not self.has_expired():  # If the particle has not expired
            # Applying gravity
            self.vel += Vector(0, -0.001)
            
            # Applying damping to gradually reduce velocity
            damping = .99
            self.vel.x *= damping
            self.vel.y *= damping
            
            # Detecting collision with walls
            if self.pos.x - self.size <= 0 or self.pos.x + self.size >= 1:
                self.vel.x *= -1  # Reflecting velocity upon collision with horizontal walls
            if self.pos.y - self.size <= 0 or self.pos.y + self.size >= 1:
                self.vel.y *= -1  # Reflecting velocity upon collision with vertical walls
            
            # Updating position
            self.pos += self.vel



# ParticleContainer Class: Manages a collection of particles
class ParticleContainer:
    def __init__(self, x_pos, y_pos):  # Initializing a particle container with given position
        self.pos = Vector(x_pos, y_pos)  # Setting the position vector
        self.particles = []  # Initializing an empty list to store particles

    def animate(self):  # Method to animate the particles
        remove_list = []  # List to hold particles to be removed
        for particle in self.particles:  # Loop through each particle in the container
            particle.move()  # Move the particle
            particle.draw()  # Draw the particle
            particle.lifetime -= 1  # Decrease particle's lifetime
            if particle.has_expired():  # If particle's lifetime has expired
                remove_list.append(particle)  # Add particle to the removal list

        for particle in remove_list:  # Loop through particles to be removed
            self.particles.remove(particle)  # Remove particle from the container


# Emitter Class: Emits particles at a certain rate
class Emitter(ParticleContainer):
    def __init__(self, x_pos, y_pos, fire_rate):  # Initializing an emitter with given position and fire rate
        super().__init__(x_pos, y_pos)  # Calling the parent class constructor
        self.fire_rate = fire_rate  # Setting the fire rate

# Firework Class: Manages a firework particle system
class Firework(ParticleContainer):
    def __init__(self, x_pos, y_pos):  # Initializing a firework particle system with given position
        super().__init__(x_pos, y_pos)  # Calling the parent class constructor
        for _ in range(500):  # Creating 500 firework particles
            self.particles.append(FireworkParticle(x_pos, y_pos, random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4), 0,
                                                  random.uniform(-0.012, -0.008), 0.004, 50))


# Marbles Class: Manages a system of marble particles
class Marbles(ParticleContainer):
    def __init__(self, x_pos, y_pos):  # Initializing a system of marble particles with given position
        super().__init__(x_pos, y_pos)  # Calling the parent class constructor
        for _ in range(10):  # Creating 10 marble particles
            self.particles.append(
                MarbleParticle(random.uniform(0.05, 1 - 0.05), random.uniform(0.05, 1 - 0.05),
                               random.uniform(-0.04, 0.04), random.uniform(-0.04, 0.04), 0,
                               random.uniform(-.002, -.001), 0.03, 500))


# Fire Class: Represents a fire emitter
class Fire(Emitter):
    def __init__(self, x_pos, y_pos, fire_rate):  # Initializing a fire emitter with given position and fire rate
        super().__init__(x_pos, y_pos, fire_rate)  # Calling the parent class constructor

    def animate(self):  # Method to animate the fire emitter
        for _ in range(self.fire_rate):  # Emitting particles based on fire rate
            self.particles.append(
                FireParticle(self.pos.x, self.pos.y, random.uniform(-0.002, 0.002), random.uniform(0.002, 0.005),
                             random.uniform(0.01, 0.03), 50))
        super().animate()


# Sparkler Class: Represents a sparkler emitter
class Sparkler(Emitter):
    def __init__(self, x_pos, y_pos, fire_rate):  # Initializing a sparkler emitter with given position and fire rate
        super().__init__(x_pos, y_pos, fire_rate)  # Calling the parent class constructor

    def animate(self):  # Method to animate the sparkler emitter
        for _ in range(self.fire_rate):  # Emitting particles based on fire rate
            self.particles.append(
                SparkParticle(self.pos.x, self.pos.y, random.uniform(-0.07, 0.07), random.uniform(-0.07, 0.07), 0.04,
                              5))
        super().animate()


def main():  # Main function to run the simulation
    dudraw.set_canvas_size(500, 500)  # Setting the canvas size
    dudraw.set_x_scale(0, 1)  # Setting the x-axis scale
    dudraw.set_y_scale(0, 1)  # Setting the y-axis scale

    objects = []  # List to hold different objects (e.g., emitters)
    objects.append(Sparkler(0.7, 0.6, 125))  # Creating a sparkler object
    objects.append(Fire(0.25, 0.25, 20))  # Creating a fire object

    while True:  # Main animation loop
        dudraw.clear(dudraw.LIGHT_GRAY)  # Clearing the canvas with a light gray color

        if dudraw.has_next_key_typed():  # Checking for keyboard input
            key = dudraw.next_key()  # Getting the next keyboard input
            if key.lower() == 'f':  # If the 'f' key is pressed
                objects.append(Firework(0.5, 0.5))  # Creating a firework object in the middle of the canvas

        if dudraw.mouse_clicked():  # Checking for mouse click
            objects.append(Marbles(0.5, 0.5))  # Creating a marble object at the mouse click position

        for obj in objects:  # Looping through each object
            obj.animate()  # Animating the object

        dudraw.show(10)  # Updating the display with a 10ms delay


if __name__ == "__main__":  # Running the main function if the script is executed directly
    main()
