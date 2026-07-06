# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The UML design would allow owners to add and manage their pets, add a care task for a pet (i.e walking, feeding, medical, grooming, etc.) Lastly it would also include the ability generate and view daily plans while filtering tasks and explaining why.

The classes included are Owner, Scheduler, Task, and Pet. Owner contains the pet owner's information and their list of pets. Pet contains a pet's profile and its list of tasks. Task represents an activity for the pet such as walking and feeding, as well as the duration and priority. Scheduler handles the pet's tasks and manages time constraints to create the plan.




**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, my design changed during implementation as my Task had no reference to the Pet it belonged to. Pet only held a list of Tasks but Tasks doesn't know this. To fix this, I decided to add a pet_name field in Task so each task can be identified independently. This would matter when Scheduler will need to work with tasks from multiple pets at once. Without this, it would be difficult to know which pet belongs to who.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considered task priority, each task's preferred time slot, daily time budget, and whether a task is recurring. Priority is the main factor in the method sort_by_priority(), since priority should matter most. Priority would focus more on a pet's health, so safety-related tasks like feeding or medication shouldn't get pushed aside. Time is used to order tasks and to catch scheduling conflicts. The time budget in the method generate_plan() lets the scheduler filter out lower-priority tasks once minutes are used up, and recurring tasks are renewed once completed.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff that my scheduler makes is that it checks for exact time matches than checking for overlapping durations. For example, a 30 minute task that starts at 9 AM and another a 9:15 AM, will overlap, but the scheduler wouldn't flag it since it only looks at start times. This is reasonable, since exact matching is faster and catches obvious scheduling mistakes, while overlap checking would need more complexity.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
