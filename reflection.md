# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design included four main classes owner, pet, task, and schedule. These classes represent the core components of the pawpal+ system and how users interact with pet care tasks.
- What classes did you include, and what responsibilities did you assign to each?
Owner
The Owner class represents the user of the system. It is responsible for managing pets and serves as the main point of interaction. It stores the owner’s information and a list of pets.
Pet
The Pet class represents an individual pet. It stores details such as name, age, breed, and medical information. It also maintains a list of tasks associated with that pet.
Task
The Task class represents a specific care activity, such as feeding or walking. It includes attributes like duration, priority, time, and status. It also contains methods to update and track task completion.
Schedule
The Schedule class is responsible for organizing tasks into a daily plan. It takes tasks from all pets and generates an ordered schedule based on priority and constraints, and provides a way to view and explain the plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time – Tasks are scheduled based on their assigned time, and conflicts are detected when tasks overlap.
Priority – Tasks are sorted so higher priority tasks High Medium Low are handled first when times are the same.
Status – Tasks can be filtered by whether they are pending or completed.
Pet association – Tasks are linked to specific pets allowing filtering by pet.
Recurrence – Some tasks repeat daily or weekly and the system automatically generates the next occurrence.
- How did you decide which constraints mattered most?
I chose these constraints based on what would be most useful for a pet owner managing daily responsibilities.
Time was the most important because scheduling depends on when tasks happen.
Priority helps decide what matters most when tasks overlap or compete.
Pet and status filtering make the app easier to use by organizing tasks clearly.
Recurrence was included because many pet care tasks (like feeding or walking) happen regularly.
I focused on keeping the system simple but practical choosing constraints that improve usability without making the logic too complex.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is using a simple conflict detection algorithm that compares every pair of tasks nested loops. This approach is not the most efficient because it has a time complexity of on^2 meaning it could slow down if there are many tasks.
- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable because the number of tasks in a pet care app is usually small. A pet owner is unlikely to have hundreds of tasks in one day so performance is not a major concern.

By using a simpler algorithm, the code is easier to read, understand, and debug. This makes it more practical for development and future updates, which is more important than optimizing performance for this scenario.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to explore how to structure classes and relationships in my PawPal+ system owner, pet, task, schedule.
- What kinds of prompts or questions were most helpful?
When a method didn’t work as expected like find_conflicts or task recurrence I asked AI to analyze the logic find mistakes and suggest fixes.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment I did not accept an AI suggestion as is was when it proposed a pythonic version of my find conflicts method using itertools.combinations and a compact list comprehension. While this version was shorter and more pythonic I found it harder to read and understand especially when trying to trace which tasks belonged to which pets.
- How did you evaluate or verify what the AI suggested?
I wrote out a few example tasks and stepped through the algorithm on paper to see if it correctly detected overlaps.

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
