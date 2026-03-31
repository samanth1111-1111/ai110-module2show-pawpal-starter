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
I tested task status updates mark_complete overdue detection is_overdue and recurring task logic next_occurrence next_task. I also tested pet task management adding removing tasks schedule sorting including untimed tasks and priority tiebreakers filtering by pet and status conflict detection overlapping adjacent cross pet and untimed tasks and task completion behavior including recurring task creation.
- Why were these tests important?
These tests are important because they verify that all core features of the scheduler work correctly and handle edge cases. They ensure tasks are ordered properly conflicts are detected accurately recurring tasks behave as expected and filtering returns the correct results. This helps make the system reliable for users managing multiple pets and schedules.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am 4/5 confident that my scheduler works correctly. The tests cover all main features like sorting filtering conflict detection recurring tasks and task completion including important edge cases like overlapping times and untimed tasks.
- What edge cases would you test next if you had more time?
I would test an owner with no pets adding duplicate pets and the update task method. I would also test more time edge cases like recurring tasks scheduled later the same day and completing the same task multiple times to ensure no unexpected behavior.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I most satisfied with the scheduler and task management. It correctly handles sorting filtering recurring tasks and conflict detection and the automated tests confirm that the logic works reliably.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
f I had another iteration I would improve the ui ux to make the task schedules and conflicts easier for users to see. I would also add more edge case tests.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that a smart backend is not enough user experience and careful testing are important ai assisted tools can speed up development and testing thoughtful design decisions are still essential for building a reliable user friendly system.
