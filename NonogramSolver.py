import z3

class Nonogram:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.solver = z3.Solver()

        self.xsize = len(columns)
        self.ysize = len(rows)

    #This code should be optimized because theorically we already have a valid solution and z3 still looks for it

    def check_solutions(self):
        if self.solver.check() == z3.sat:
            self.model = self.solver.model()
            current_solution = []
            for v in self.model:
                current_solution.append(v() != self.model[v])
            self.solver.add(z3.Or(current_solution))

            with open("currentsolution.txt", "a") as fp:
                fp.write("Test:\n%s\n" % current_solution)
            #   f = open("currentsolution.txt", "a")
            #   f.write(current_solution)
            #   f.close
            if self.solver.check() == z3.sat:
                return False #Not an unique solution
            else:
                return True  #Unique solution
        else: #This line of code should never be reached, unless the nonogram has no solution
            print("Error")
            return False

    def setup_vars(self, nums, prefix, size):
        results = []
        for i in range(len(nums)):
            vs = z3.Int("%s,%d,s" % (prefix, i+1))
            ve = z3.Int("%s,%d,e" % (prefix, i+1))
            self.solver.add(ve-vs == nums[i]-1)
            self.solver.add(vs >= 0)
            self.solver.add(ve < size)
            results.append((vs,ve))

        for i in range(len(nums)-1):
            ve0 = results[i][1]
            vs1 = results[i+1][0]
            self.solver.add(vs1 >= ve0+2)

        return results

    def setup_cell_constraints(self, cells, cvars):
        for i in range(len(cells)):
            rule_i = z3.Or([z3.And(vs <= i, i <= ve) for (vs,ve) in cvars])
            self.solver.add(cells[i] == rule_i)

    def solve(self):
        self.cells = [[z3.Bool("cell[%d,%d]" % (x+1,y+1)) for x in range(self.xsize)] for y in range(self.ysize)]

        self.column_vars = [
            self.setup_vars(self.columns[i], "c%d" % (i+1), self.ysize)
            for i in range(self.xsize)
        ]
        self.row_vars = [
            self.setup_vars(self.rows[i], "r%d" % (i+1), self.xsize)
            for i in range(self.ysize)
        ]

        for i in range(self.xsize):
            self.setup_cell_constraints([row[i] for row in self.cells], self.column_vars[i])

        for i in range(self.ysize):
            self.setup_cell_constraints(self.cells[i], self.row_vars[i])

        return self.check_solutions()