class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s

    def classify_chomsky_hierarchy(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for left, right in self.p.items():
            for production in right:
                # Check Type 3 (Regular Grammar)
                if not (len(left) == 1 and left in self.vn and
                        (len(production) == 1 and production[0] in self.vt or
                         len(production) == 2 and production[0] in self.vt and production[1] in self.vn)):
                    is_regular = False

                # Check Type 2 (Context-Free Grammar)
                if len(left) > 1:
                    is_context_free = False

                # Check Type 1 (Context-Sensitive Grammar)
                if len(left) > len(production):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3: Regular Grammar"
        elif is_context_free:
            return "Type 2: Context-Free Grammar"
        elif is_context_sensitive:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"