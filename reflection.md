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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
