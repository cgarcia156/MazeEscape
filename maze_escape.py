# Author    : Christian Garcia
# Project   : Maze Escape
# Input     : Text file containing the maze
# Processing: Find the direction to escape from any point
# Output    : Display the solved maze

def main():
  filename = input("Enter the name of the maze file: ")

  try:
    mazeList = readMaze(filename)
    neighbors = buildNeighborDict(mazeList)
    escapePath = {}

    # Initialize escapePath
    for key in neighbors:
      escapePath[key] = '?'

    # Update locations on the borders
    updated = solveBoundary(escapePath, mazeList)
    # Update neighbors while there are neightbors to update
    while updated:
      updated = updateNeighbors(updated, escapePath, neighbors)

    # Print the final result
    printMaze(mazeList, escapePath)
  
  except IOError:
    print("Error: File Not Found")
  
  except RuntimeError as error:
    print("Error:", error)
          
def updateNeighbors(locations, escapePath, neighbors):
  """
  Updates the escape path for neighboring locations

      Parameters:
          locations(list) - list of locations that were recently updated
          escapePath(dict) - the escape path dictionary
          neighbors(dict) - the dictionary containing neighbors of each corridor
      
      Returns:
          list containing all the updated locations
  """
  updatedLocations = []
  tempDict = {}

  for key in locations:
    # Make sure location has an escape path
    if escapePath[key] != '?':
      for neighbor in neighbors[key]:
        # Make sure neighbor doesn't have a path yet
        if escapePath[neighbor] == '?':
          # Add to list of updated locations
          updatedLocations.append((neighbor))
          # Check if path should be N, S, W, or E
          row,col = neighbor
          if row - 1 == key[0]:
            tempDict[neighbor] = 'N'
          elif row + 1 == key[0]:
            tempDict[neighbor] = 'S'
          elif col - 1 == key[1]:
            tempDict[neighbor] = 'W'
          else:
            tempDict[neighbor] = 'E'

  # Update escape path
  for key in tempDict:
    escapePath[key] = tempDict[key]

  return updatedLocations
  
def solveBoundary(escapePath, mazeList):
  """
  Updates the values of boundary locations

      Parameters:
          escapePath(dict)
  """
  updatedLocations = []
  rows = len(mazeList)
  cols = len(mazeList[0])

  for i,j in escapePath:
    # If location is at the very top
    if i == 0:
      escapePath[(i,j)] = 'N'
      updatedLocations.append((i,j))
    # If location is at the very bottom
    elif i == rows-1:
      escapePath[(i,j)] = 'S'
      updatedLocations.append((i,j))
    # If location is to the furthest right
    elif j == cols-1:
      escapePath[(i,j)] = 'E'
      updatedLocations.append((i,j))
    # If location is to the furthest left
    elif j == 0:
      escapePath[(i,j)] = 'W'
      updatedLocations.append((i,j))

  return updatedLocations

def buildNeighborDict(mazeList):
  """
  Creates a dictionary containing all the neighbors of each location
  Table contains 1's and 0's. 1 = location exists

      Parameters:
          mazeList(list) - maze is represented as a list of lists

      Returs:
          A dictionary containing all the neighbors of each location
  """
  maze = {}
  for row in range(len(mazeList)):
    for col in range(len(mazeList[0])):
      if mazeList[row][col]:
        neighbors = set()
        # Add neighbor above if it exists
        if row > 0:
          if mazeList[row-1][col]:
            neighbors.add((row-1, col))
        # Add neighbor to the right if it exists
        if col < len(mazeList[0])-1:
          if mazeList[row][col+1]:
            neighbors.add((row, col+1))
        # Add neighbor below if it exists
        if row < len(mazeList)-1:
          if mazeList[row+1][col]:
            neighbors.add((row+1, col))
        # Add neighbor to the left if it exists
        if col > 0:
          if mazeList[row][col-1]:
            neighbors.add((row, col-1))
        
        # Set location to map to all neighbors
        maze[(row, col)] = neighbors

  return maze

def readMaze(filename):
  """
  Reads a file containing a maze into a list of lists
   '*' = wall and ' ' = corridor

      Parameters:
          filename(str) - name of the input file

      Returns:
          a list of lists, '*' -> 0, ' ' -> 1
          
  """
  maze = []
  size = 0
  first = True

  with open(filename, 'r') as infile:
    for line in infile:
      # Remove newline character
      line = line.rstrip('\n')

      # Set/Check the size
      if first:
        size = len(line)
        first = False
      elif len(line) != size:
        raise RuntimeError("Invalid Data")

      # Create row and add to maze list
      row = []
      for loc in line:
        if loc == '*':
          row.append(0)
        elif loc == ' ':
          row.append(1)
        else:
          raise RuntimeError("Invalid File Contents")
      maze.append(row)

  return maze

def printMaze(maze, escapePath):
  """
  Prints the maze with the direction to escape at any point

      Parameters:
          maze(list) - maze is represented as a list of lists

  """
  for row in range(len(maze)):
    for col in range(len(maze[0])):
      if (row,col) in escapePath:
        print(escapePath[(row,col)], end="")
      else:
        print('*', end="")
    print()

main()
