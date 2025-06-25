from logic import *

# Propositional symbols for each character
AKnight = Symbol("A is a Knight")
AKnave  = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave  = Symbol("B is a Knave")
CKnight = Symbol("C is a Knight")
CKnave  = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Domain rule: A is exactly one of knight or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A's statement: "AKnight and AKnave"
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."  B says nothing.
knowledge1 = And(
    # Domain rules for A and B
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),

    # A's statement: "AKnave and BKnave"
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
same = Or(And(AKnight, BKnight), And(AKnave, BKnave))
diff = Or(And(AKnight, BKnave),  And(AKnave, BKnight))
knowledge2 = And(
    # Domain rules for A and B
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),

    # A's statement: "same"
    Implication(AKnight, same),
    Implication(AKnave, Not(same)),

    # B's statement: "diff"
    Implication(BKnight, diff),
    Implication(BKnave, Not(diff))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave." (unknown which).
# B says "A said 'I am a knave'." and "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Domain rules for A, B, C
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave), Not(And(CKnight, CKnave)),

    # B's first statement: "A said 'AKnave'"
    Implication(BKnight, AKnave),
    Implication(BKnave, Not(AKnave)),

    # B's second statement: "CKnave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C's statement: "AKnight"
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for title, kb in puzzles:
        print(title)
        for s in symbols:
            if model_check(kb, s):
                print(f"    {s}")

if __name__ == "__main__":
    main()
