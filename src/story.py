STORY = {
    "Introduction":  [
        "Welcome to the town of Sunnyvale, whose citizens are obsessed with all things avocado. They put them on their eggs in the morning, in their tacos midday, and transform them into guacamole for the evening. Everyone agrees that guacamole is the best use of the beloved avocado, but that’s about the only thing they can agree on. No one can agree whose guacamole recipe is the best, with most insisting it’s how their mama does it!",
        "Sensing an opportunity for some friendly competition, Mayor Michelada suggests the town hold a contest to settle once and for all who can make the best guac. Anyone who thinks their recipe is particularly special can bring a bowl of their best stuff to the town plaza this Sunday. The town will gather, try each one, and vote for the best! Everyone loves the idea. People immediately start signing up and texting their friends to do so too.",
        "That Sunday, the whole town – 250 people! – shows up for the contest. Everyone’s excited to get to spend the afternoon indulging in their favorite dip while playing food critic. The entrants, twenty three people with big bowls of their family’s pride and joy, gather in the center of the plaza.",
    ],

    "Guac God": [
        "Looking down from Horchata Heaven, you are the Guacamole God. You are so pleased that the beings of your creation have fallen for your favorite dip and also proud of their embrace of democratic values. And while you admire everyone’s hard work, since you are hors d'oeuvre omniscient, you can already clearly spot the winner.",
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
        "But how should they pick who gets to be a taster? Well, one of the few things everyone can agree on is that their mom makes the best guac. Maybe they just the mom’s vote? That could work. But people will be upset if they came all this way and don’t get to try any guac. And, truthfully, the Mayor knows his townspeople. They like to have their own say in the matter, especially the younger ones. Almost on principle they’re going to disagree with whatever their parents say!",
        "Seeing the distress on her Mayor’s face, Earnest Emilia approaches with an idea. She’s just taken an online course in data analytics and really enjoyed learning the clever ways purposeful randomness can useful. What if not everyone needs to try every guac, she suggests. What if, we intentionally let people only try some, but randomly assign a different some to each person?",
    ]

    # "Voter Types":  [
    #     "You think for a minute on whether the townspeople would agree of your assessment of which is best? You know some people, like Precocious Pepe, like guac so much that they’ll probably score every entrant generously. Others, like Finicky Francisca, are quite critical and will have no problem picking out flaws. They’ll probably score things quite harshly. But as you watch everyone set up, you’re pretty confident that most people will assess the submissions fairly, give or take a few points. The only person you’re really worried about is Cliquey Carlos. He’s the ring leader of a pretty loyal group of farmers. Plus, he always throws the best parties! It’s pretty clear anyone who wants to stay on his good side is going to be voting for him.",
    # ],

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
    ]
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
            "Success!"
        ],
        False:  [
            "Oh no!"
        ]
    }
    
}