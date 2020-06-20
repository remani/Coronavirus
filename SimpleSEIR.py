import numpy as np


class SEIRModel:

    def __init__(self, s, e, i, r, m, n, l, inf, b):
        self.susceptible = s
        self.exposed = e
        self.infected = i
        self.removed = r
        self.mu = m
        self.nu = n
        self.alpha = 1 / l
        self.gamma = 1 / inf
        self.beta = b

    def projectSEIR(self, n):
        s = np.array([self.susceptible])
        e = np.array([self.exposed])
        i = np.array([self.infected])
        r = np.array([self.removed])

        for j in range(n):
            pop = s[j] + e[j] + i[j] + r[j]
            sToE = np.around(self.beta(j) * s[j] * i[j] / pop)
            eToI = np.around(self.alpha * e[j])
            iToR = np.around(self.gamma * i[j])

            s = np.append(s, np.around((1 - self.nu) * s[j]) - sToE
                          + np.around(self.mu * pop))
            e = np.append(e, np.around((1 - self.nu) * e[j]) + sToE - eToI)
            i = np.append(i, np.around((1 - self.nu) * i[j]) + eToI - iToR)
            r = np.append(r, np.around((1 - self.nu) * r[j]) + iToR)

        return (s, e, i, r)

    def projectSEIRS(self, n, immunityLength):
        s = np.array([self.susceptible])
        e = np.array([self.exposed])
        i = np.array([self.infected])
        r = np.array([self.removed])
        eps = 1 / immunityLength

        for j in range(n):
            pop = s[j] + e[j] + i[j] + r[j]
            sToE = np.around(self.beta(j) * s[j] * i[j] / pop)
            eToI = np.around(self.alpha * e[j])
            iToR = np.around(self.gamma * i[j])
            rToS = np.around(eps * r[j])

            s = np.append(s, np.around((1 - self.nu) * s[j]) + rToS - sToE
                          + np.around(self.mu * pop))
            e = np.append(e, np.around((1 - self.nu) * e[j]) + sToE - eToI)
            i = np.append(i, np.around((1 - self.nu) * i[j]) + eToI - iToR)
            r = np.append(r, np.around((1 - self.nu) * r[j]) + iToR - rToS)

        return (s, e, i, r)

    # Assumes birth and death rates are negligible
    def projectSEIRConstantPop(self, n):
        s = np.array([self.susceptible])
        e = np.array([self.exposed])
        i = np.array([self.infected])
        r = np.array([self.removed])
        pop = self.susceptible + self.exposed + self.infected + self.removed

        for j in range(n):
            sToE = np.around(self.beta(j) * s[j] * i[j] / pop)
            eToI = np.around(self.alpha * e[j])
            iToR = np.around(self.gamma * i[j])

            s = np.append(s, s[j] - sToE)
            e = np.append(e, e[j] + sToE - eToI)
            i = np.append(i, i[j] + eToI - iToR)
            r = np.append(r, r[j] + iToR)

        return (s, e, i, r)

    # Assumes birth and death rates are negligible
    def projectSEIRSConstantPop(self, n, immunityLength):
        s = np.array([self.susceptible])
        e = np.array([self.exposed])
        i = np.array([self.infected])
        r = np.array([self.removed])
        pop = self.susceptible + self.exposed + self.infected + self.removed
        eps = 1 / immunityLength

        for j in range(n):
            sToE = np.around(self.beta(j) * s[j] * i[j] / pop)
            eToI = np.around(self.alpha * e[j])
            iToR = np.around(self.gamma * i[j])
            rToS = np.around(eps * r[j])

            s = np.append(s, s[j] + rToS - sToE)
            e = np.append(e, e[j] + sToE - eToI)
            i = np.append(i, i[j] + eToI - iToR)
            r = np.append(r, r[j] + iToR - rToS)

        return (s, e, i, r)
