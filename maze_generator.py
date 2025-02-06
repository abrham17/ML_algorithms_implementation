from pyamaze import maze , agent

def draw_maze(x_length , y_length):
    m = maze(x_length , y_length)
    m.CreateMaze()
    a = agent(m , footprints=True, filled = True , color = 'red' )
    return m , a

m , a = draw_maze(15,20)
m.run()
print(m.grid)