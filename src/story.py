from re import M


STORY = {
    "Introduction":  [
        "Welcome to the town of Sunnyvale, whose citizens are obsessed with all things avocado. They put them on their eggs in the morning, in their tacos midday, and transform them into guacamole for the evening. Everyone agrees that guacamole is the best use of the beloved avocado, but that’s about the only thing they can agree on. No one can agree whose guacamole recipe is the best, with most insisting it’s how their mama does it!",
        "Sensing an opportunity for some friendly competition, Mayor Michelada suggests the town hold a contest to settle once and for all who can make the best guac. Anyone who thinks their recipe is particularly special can bring a bowl of their best stuff to the town plaza this Sunday. The town will gather, try each one, and vote for the best! Everyone loves the idea. People immediately start signing up and texting their friends to do so too.",
        "That Sunday, the whole town – 250 people! – shows up for the contest. Everyone’s excited to get to spend the afternoon indulging in their favorite dip while playing food critic. The entrants, twenty people with big bowls of their family’s pride and joy, gather in the center of the plaza.",
    ],

    "Guac God": [
        "Looking down from Horchata Heaven, you are the Guacamole God. You are so pleased that the beings of your creation have fallen for your favorite dip and also proud of their embrace of democratic values. And while you admire everyone’s hard work, since you are hors d'oeuvre omniscient, you can already clearly spot the winner.",
    ],

    "demo_voting":  [
        "Above you’ve selected how each guacamole in this contest should objectively be scored, but the townspeople of Sunnyvale are not computers. They’ll have their own subjective opinions. Luckily they’re pretty reasonable and will tend to agree with your assessment, plus or minus a point or two. Click below to see how a few townspeople will judge some of the submissions.",
    ],

    "simulation_1":   [
        "Mayor Michelada is busy handing out bowls of tortilla chips. Obviously, if this is going to be a fair competition, everyone is going to need to use the same kind of chip. He also begins handing out the score cards so people can score each guac on a scale from 1 to 10. He thought about asking everyone to try each guac and and then sorting them from worst to best, but there are just too many guacs! Try to keep track of 20 different guacamoles would be too hard. It’ll much easier for people to just score them independently and then add up the scores. Whichever guac gets the highest score wins! Easy enough.",
        "For a moment, Mayor Michelada worries that perhaps 20 guacamoles is too many. Do people have that much room in their stomachs? Will everyone just prefer the first one they try, when they’re the most hungry? Then, by the time they’re full, will they all think the last one is nothing special? But looking around at the huge crowd as everyone jockeys to get close, he realizes that folks will end up tasting in different orders, so hopefully people getting full at different times will just even itself out.",
        ],

    "transition_1_to_2":    [
        "The last contest worked well because everyone who participated got to try every single guacamole entrant. But is that realistic? Over two hundred people showed up to join in the fun! Can we have expected that those who entered teh contest made enough guac to feed that many people? Let’s imagine another version of these events.",
    ],

    "simulation_2":   [
        "Mayor Michelada looks around at the huge crowd that’s gathered. He’s thrilled so many people were excited by his idea for a contest, but he’s wishing he had told the entrants to make more guacamole. Will they have enough to go around? Heck, they might run out of chips! He is sweating trying to figure out how they can save the competition. Clearly they’re going to have to limit how many people can participate – there’s just no way for everyone to try everything!",
        "But how should they pick who gets to be a taster? Well, one of the few things everyone can agree on is that their mom makes the best guac. Maybe just only moms vote? That could work. But people will be upset if they came all this way and don’t get to try any guac. And, truthfully, the Mayor knows his townspeople. They like to have their own say in the matter, especially the younger ones. Almost on principle they’re going to disagree with whatever their parents say!",
        "Seeing the distress on her Mayor’s face, Earnest Emilia approaches with an idea. She’s just taken an online course in data analytics and really enjoyed learning the clever ways purposeful randomness can useful. What if not everyone needs to try every guac, she suggests. What if, we intentionally let people only try some, but randomly assign a different some to each person?",
    ],

    "simulation_2_a": [
        "Now that we've injected a certain amount of randomness into the contest, it's possible that it could turn out different ways if done different times. Let's see what would happen if we help this same contest 100 times.",
    ],

    "transition_2_to_3":    [
        "The previous contest worked well, to a point. You may have seen that when there is one clear winner among the guacamoles, we can limit how many guacs each voter tastes to a pretty small number. That could help stretch a limited amount of dip across a huge audience of participants. But as the race got closer and closer, limiting the sample of the contest each person gets to try starts to affect the results.",
        "Our previous simulations also assumed every person had more or less the same opinions of each guac, with slight variations for how hungry or full they were by the time they tried each one. Is that realistic? Let’s try again, and this time meet some of our townspeople!",
    ],

    "simulation_3": [
        "Up in Horchata Heaven, walking through your fields on celestial cilantro, you wonder for a minute whether the townspeople would agree with your assessment of how the guacamoles compare to each other. You know some people, like Perky Pepe, like guac so much that they’ll probably score every entrant generously. Others, like Finicky Francisca, are quite critical and will have no problem picking out flaws. They’ll probably score things quite harshly. Hopefully, folks like them won’t skew the results too much. The only person you’re really worried about is Cliquey Carlos. He’s the ring leader of a pretty loyal group of farmers. Plus, he always throws the best parties! It’s pretty clear anyone who wants to stay on his good side is going to be voting for him no matter how good his guac actually is.",
    ],

    "condorcet_1":  [
        "Our Mayor designed the ballots so that tasters score each guac on a scale from one to ten, with one for barely edible and ten for the best guacamole of all time. This was as opposed to asking tasters to sort all the guacs they tried from worst to best. His thinking was that with so many entrants in the competition, keeping track of how all those guacamoles compare to each other would be too mentally taxing. Much easier to simply ask people rate them independently. That way they can just enjoy the guac party and not get all confused keeping track of their ballot. A big assumption baked into this method, however, is that people don’t let their experience with one guac affect their vote of another guac.",
        "Imagine Pepe, who loves all guac but is trying his best to be a fair voter. The first guac he tries, he just loves. Scores it a nine. The next guac he tries just knocks his socks off. Wow, didn’t know guacamole could be made that good. Scores it a ten. But wait, it’s definitely more that just one point better than that first one. Better revise that down to a seven.",
        "The problem with our Mayor’s naive attempt at a simple one through ten scale is that no one has a fixed understanding of how good the ten is or how bad the one is. People will naturally develop their mental scale by comparing all the guacs they’ve tried. So, as Emilia explains to him over a late night Topo Chico after the big contest as wrapped up, it’s better to interpret people’s ballots not as raw scores but as implicit rankings.",
        "She grabs a napkin to make herself more clear. Imagine someone submits a ballot like this:",
    ],

    "condorcet_2": [
        "This person only got to taste five guacamoles, giving them scores of 8, 4, 4, 6, and 1. From this, it’s probably not right to say Guac#2 is twice as good as Guac#4. But we can definitely say, of the guacamoles that this person got to try, they think #2 was the best, #15 was second best, #4 and #7 were equally mediocre, and #20 was crap.",
        "So for next year, Emilia suggests, we could use the same ballots, but look at each one as a short list of rankings. Then, instead of adding up all the scores, we collect all the short lists of rankings into one grand list of rankings. We wouldn’t be able to tally by hand anymore; she’ll have to write some code to do it. But that will be even faster anyway!",
    ],

    # "Unknown Best":  [
    #     "What if we don't know who is the best and just decide to go with people's guts? On day 1 of the competition everyone tries all the guacs, and a winner is found. However, the judges realize that trying all guacs turns out to be way too much food. So, on day two they decide to do an experiment. What if we only assign to each judge a random subset of guacs? How small does this subset have to be before the winner identify on day 1 is lost?",
    # ],

    # "Conclusion 1":  [
    #     "When all guacs are relatively similar, the votes end up being very close to each other. As a result, as soon as we start fractioning the guacs it's easy to loose the winner. Try it!"
    # ],

    # "Conclusion 2":  [
    #     "Introducing better/worse ingredients leads to clearer winners, even when not everyone tries all the guacs."
    # ]
}


INSTRUCTIONS = {
    "Guac God": [
        "Objectively, how do the guacs measure up, relative to each other? Choose a scenario below to be used throughout this simulation.",
    ],

    "simulation_1": [
        "In our first contest, tasters slightly prefer the guacamoles they try earliest and like them less and less as they get more full. But, all participants taste in random orders and everyone tries every guacamole. Click the button below to simulate the voting process. Highest score wins!"
    ],

    "simulation_2": [
        "In our second contest, try limiting how many guacamoles each taster gets to try. Like before, tasters will taste in random orders and get slightly less generous with their scores as they get full."
    ],

    "simulation_3_a": [
        "Choose what percentage of of the town is like each character.",
    ],

    "simulation_3_b": [
        "In our third contest, the town will vote differently depending on how many of type of person you chose above. Like before, you can also try limiting how many guacamoles each person gets to sample.",
    ],

    "condorcet_1": [
        "In our next contest, we’ll be tallying ballots using Emilia’s new method of comparing implicit rankings, but you can control all the same parameters.",
    ],

    "condorcet_2": [
        "Set how many guacamoles each person gets to try.",
    ],
}


SUCCESS_MESSAGES = {
    "simulation_1": {
        True:  [
            "Success! Even though people had so many guacs to try, and probably became quite full by the end, having everyone taste in random orders ensured the contest still had a fair result.",
            ],
        False:  [
            "Oh no! The contest didn't reach a fair conclusion. That's not supposed to happen!"
        ]
    },

    "simulation_2": {
        True:   [
            "Success! Even though the tasters missed out on trying MISSING_GUACS guacs each, we had enough participants that we still reached a fair result.",
            "Try again! Can we push that number even lower than GUAC_LIMIT still get a fair result?"
        ],
        False:  [
            "Oh no! Looks like missing out on trying MISSING_GUACS guacs each was too many to skip. Perhaps if we had more tasters we could've compensated."
        ]
    },

    "simulation_3": {
        True:  [
            "Success!",
            ],
        False:  [
            "Oh no!"
        ]
    },

    "100_times": {
        True:   [
            "Across 100 simulations, NAME still took home the trophy more than anyone else, winning PERCENT of the contents. Take a look at who else took home the trophy at times and whether or not their guacamole deserved the win.",
        ],
        False:  [
            "Across 100 simulations, NAME took home the trophy more than anyone else, but they did so less than half the time. In PERCENT of our contents, someone other than whom you decided had the best guacamole took home the win. Take a look at who they were and if they deserved it.",
        ],
    },

    "condorcet": {
        True:  [
            "Success!",
            ],
        False:  [
            "Oh no!"
        ]
    },
    
}