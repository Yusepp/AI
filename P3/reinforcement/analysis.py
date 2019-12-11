# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question3():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE' #
    
    # Atfter few tries I noticed that increasing the learning rate maybe noticed as getting closer to cross the bridge but #unfortunetly it does not cross it so he learns to win with the closest terminal state.
    #Putting an epsilon of 0 will make the agent go straight to the terminal state all time.
    #So in the end there's no combination of epsilon and lr that allows to find the optimal policy after 50 tries.
    
if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
