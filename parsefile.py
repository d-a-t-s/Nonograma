def parsefile(file_path):
    grid = []
    with open(file_path, "r") as file:
        grid_size = file.readline().strip().split(';')
        width, height = int(grid_size[0]), int(grid_size[1])
        
        palette = []
        for i in range(4):
            line = file.readline().strip().split(';')
            palette.append((int(line[1]), int(line[2]), int(line[3])))

        for line in file.readlines():
             line = line.strip()
             if line:
                  pixel = line.split(';')
                  x, y, color = pixel[:3]
                  grid.append((int(x), int(y), int(color)))  
    
    return width, height, palette, grid

def Colored_grid(route_picture):
    width, height, palette, info_grid = parsefile(route_picture)
    grid = []
    
    length = len(info_grid)
    for i in range(info_grid[length-1][1] + 1):
        row = []
        for j in range((info_grid[length-1][0] + 1) * i , (info_grid[length-1][0] + 1) * (i+1), 1):
            row.append(info_grid[j][2])
        grid.append(row)
    return palette,grid