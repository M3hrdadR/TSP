from Ant_System import AS

if __name__ == '__main__':
    n = int(input("Please enter number cities:"))
    tsp_as = AS(n, n)
    tsp_as.main_loop()
