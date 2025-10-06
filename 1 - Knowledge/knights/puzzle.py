from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # --- Exactly-one role for each person ---
    Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave)),

    # --- A's statement: "I am both a knight and a knave."
    # If A is a knight, then this statement (AKnight ∧ AKnave) must be true;
    # if A is a knave, then the statement must be false.
    Biconditional(AKnight, And(AKnight, AKnave))
    # Implication(AKnight, And(AKnight, AKnave)),
    # Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # --- Exactly-one role for each person ---
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    # --- A's statement: "We are both knaves."  
    # If A is a knight, then this statement must be true;  
    # if A is a knave, then this statement must be false.
    Biconditional(AKnight, And(AKnave, BKnave))
    # Implication(AKnight, And(AKnave, BKnave)),
    # Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # --- Exactly-one role for each person ---
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # --- A's statement: "We are the same kind."
    # If A is a knight, then (A and B are both knights OR both knaves) must be true;
    # if A is a knave, then that statement must be false.
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # --- B's statement: "We are of different kinds."
    # If B is a knight, then (one is a knight and the other a knave) must be true;
    # if B is a knave, then that statement must be false.
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # --- Exactly-one role for each person ---
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # --- Model WHICH sentence A uttered via two branches ---
    # Branch 1: A said "I am a knight." → B's claim ("A said knave") is false ⇒ B is a knave
    # Branch 2: A said "I am a knave."  → B's claim is true ⇒ B is a knight
    Or(
        And(
            Biconditional(AKnight, AKnight),  # truth-link if A uttered "I am a knight"
            BKnave                            # then B's claim is false
        ),
        And(
            Biconditional(AKnight, AKnave),   # truth-link if A uttered "I am a knave"
            BKnight                           # then B's claim is true
        )
    ),

    # --- B's second statement: "C is a knave." ---
    Biconditional(BKnight, CKnave),

    # --- C's statement: "A is a knight." ---
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
