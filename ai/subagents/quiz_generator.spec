# Quiz Generator Subagent Specification

## Name
Quiz Generator

## Purpose
Generate quizzes and exercises based on book content for the Physical AI & Humanoid Robotics book to help users test their knowledge.

## Inputs
- `topic`: Main topic for the quiz (e.g., "ROS2 Fundamentals", "Gazebo Simulation", "NVIDIA Isaac", "VLA Systems")
- `difficulty_level`: Difficulty level (e.g., "beginner", "intermediate", "advanced")
- `question_count`: Number of questions to generate
- `question_types`: Types of questions to include (e.g., "multiple_choice", "true_false", "short_answer", "code_review")
- `learning_objectives`: Specific learning objectives to assess
- `source_content`: Content from which to draw questions

## Outputs
- `quiz_questions`: Array of quiz questions with answers
- `explanation`: Detailed explanations for each answer
- `scoring_guide`: Guidelines for scoring and assessment
- `learning_assessment`: Mapping of questions to learning objectives

## Constraints
- Questions must be based on actual book content
- Difficulty must match the specified level
- Questions should assess understanding, not just memorization
- All questions must have clear, unambiguous answers
- Include practical application questions for advanced levels

## Acceptance Criteria
- Questions are relevant to the specified topic
- Difficulty level matches the requested level
- Questions assess actual understanding of concepts
- All questions have clear, correct answers
- Explanations are detailed and educational

## Example Input
```
{
  "topic": "ROS2 Fundamentals",
  "difficulty_level": "intermediate",
  "question_count": 5,
  "question_types": ["multiple_choice", "code_review"],
  "learning_objectives": ["understand ROS2 architecture", "know how to create nodes"],
  "source_content": "Content from ROS2 chapters..."
}
```

## Example Output
```
{
  "quiz_questions": [
    {
      "question": "What is the main purpose of the ROS2 DDS implementation?",
      "type": "multiple_choice",
      "options": ["A) To provide a GUI for ROS2", "B) To enable communication between nodes", "C) To manage robot hardware", "D) To store robot data"],
      "correct_answer": "B",
      "explanation": "ROS2 uses DDS (Data Distribution Service) as the middleware for enabling communication between nodes..."
    }
  ],
  "explanation": "Detailed explanations for each question...",
  "scoring_guide": "Scoring guidelines...",
  "learning_assessment": "Mapping of questions to objectives..."
}
```

## Implementation Notes
- Use book content as the basis for questions
- Include practical scenarios for higher difficulty levels
- Ensure questions test comprehension, not just recall
- Provide educational explanations that reinforce learning
- Include code-based questions for technical topics