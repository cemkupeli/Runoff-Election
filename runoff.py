import sys
import csv

def main():
    # The list storing the preferences (rankings) of the voters
    preferences = []

    # The list storing the candidates information
    candidates = []

    # The number of candidates
    numCandidates = 0

    # The number of votes
    numVotes = 0

    # The name of the program, the name of the file storing the results, and at least two candidate names must be provided as arguments
    if len(sys.argv) < 4:
        print("Usage: python runoff.py results_file candidate1 candidate2 candidate3 ...")
        return

    numCandidates = len(sys.argv) - 2

    # Populates the list of candidates
    for i in range(len(sys.argv) - 2):
        candidate = {"name": sys.argv[i + 2], "votes": 0, "isEliminated": False}
        candidates.append(candidate)

    # Opens the results CSV file
    with open(sys.argv[1]) as results_file:
        reader = csv.DictReader(results_file)

        print("\nProcessing the ballots...")
        # Appends each ballot (as a list in descending order of preference) to the preferences list
        ballotCount = 0
        for row in reader:

            ballot = [""] * len(candidates)
            ballotCount += 1

            for candidate in candidates:
                preference = row[candidate["name"]]
                if preference != "":
                    preferenceNum = int(row[candidate["name"]])
                    ballot[preferenceNum - 1] = candidate["name"]

            if isValid(ballot, numCandidates):
                numVotes += 1
                preferences.append(ballot)
            else:
                print("Invalid ballot (row " + str(ballotCount + 1) + ")")

        print("Finished processing ballots.")
        print("Number of valid votes: " + str(numVotes))
        # print("Preferences:")
        # for preference in preferences:
        #     print(preference)

    # Tabulates the votes and checks if there is a winner until a winner is found
    countingRound = 0
    while True:
        countingRound += 1
        print("\nCOUNTING ROUND " + str(countingRound))

        # Tabulates the votes for the current round (the value returned is the number of active votes)
        numVotes = tabulate(candidates, preferences)

        # Displays the votes that each candidate has in the current round (as well as the total active votes)
        print("Number of active votes: " + str(numVotes))
        print("Current votes:")
        for candidate in candidates:
            if not candidate["isEliminated"]:
                print(candidate["name"] +  ": " + str(candidate["votes"]))
            else:
                print(candidate["name"] + ": --")

        # Checks if there is a winner
        won = printWinner(candidates, numVotes)
        if won:
            break

        # Records the minimum number of votes received by any candidate
        minVotes = findMin(candidates, numVotes)

        # Checks if there is a tie
        tie = isTie(minVotes, candidates)
        if tie:
            print("\nRESULT - Tie")
            for candidate in candidates:
                if not candidate["isEliminated"]:
                    print(candidate["name"] + "\n")
            break

        # Eliminates every candidate that has the minimum number of votes
        eliminate(minVotes, candidates)

# Calculates the votes for each candidate in the current state of the election
def tabulate(candidates, preferences):
    # Resets vote counts
    for candidate in candidates:
        candidate["votes"] = 0

    # The number of votes cast for continuing candidates
    activeVotes = 0

    # Processes each ballot
    for ballot in preferences:
        # print(ballot)
        voteCounted = False
        # Processes each rank until a vote is counted
        for i in range(len(candidates)):
            # If a vote has already been counted from this ballot, moves onto the next ballot
            if voteCounted == True:
                break
            else:
                # Determines which candidate the vote at the current rank is for, counts the vote if the candidate is not eliminated
                for candidate in candidates:
                    if ballot[i] == candidate["name"] and not candidate["isEliminated"]:
                        # print("The vote goes to: " + candidate["name"])
                        candidate["votes"] += 1
                        activeVotes += 1
                        voteCounted = True
    return activeVotes

# Determines a winner, prints the name and returns True if there is one, returns False if not
def printWinner(candidates, numVotes):
    # Win condition: Having more than half the votes
    WIN_CONDITION = numVotes // 2 + 1

    for candidate in candidates:
        if candidate["votes"] >= WIN_CONDITION:
            print("\nRESULT - Win")
            print("The winner of the election is " + candidate["name"] + "\n")
            return True

    return False

# Finds the minimum number of votes received by any candidate in the current round
def findMin(candidates, numVotes):
    minVotes = numVotes

    for candidate in candidates:
        if candidate["votes"] < minVotes and not candidate["isEliminated"]:
            minVotes = candidate["votes"]

    return minVotes

# Determines if there is a tie
def isTie(minVotes, candidates):
    for candidate in candidates:
        if candidate["votes"] != minVotes and not candidate["isEliminated"]:
            return False
    return True

# Checks if a ballot is valid (no skipped preference)
def isValid(ballot, numCandidates):
    # Starting from the last rank, iterates until a choice is found
    for i in range(numCandidates):
        if ballot[-1 * (i + 1)] != "":
            for j in range(numCandidates - i):
                if ballot[-1 * (i + 1 + j)] == "":
                    return False
            return True
    return True

# Eliminates all candidates that have the minimum number of votes
def eliminate(minVotes, candidates):
    for candidate in candidates:
        if candidate["votes"] == minVotes:
            print("Eliminated candidate: " + candidate["name"])
            candidate["isEliminated"] = True

main()