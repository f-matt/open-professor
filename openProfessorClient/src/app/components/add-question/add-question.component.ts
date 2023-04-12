import { Component } from '@angular/core';
import { Question } from 'src/app/models/question.model';
import { Answer } from 'src/app/models/answer.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { QuestionsService } from 'src/app/services/questions.service';

@Component({
  selector: 'app-add-question',
  templateUrl: './add-question.component.html',
  styleUrls: ['./add-question.component.css']
})
export class AddQuestionComponent {

  constructor(private snackBar : MatSnackBar,
    private questionsService : QuestionsService) {}

  question : Question = new Question();
  correctAnswer : Answer = new Answer();
  wrongAnswer1 : Answer = new Answer();
  wrongAnswer2 : Answer = new Answer();
  wrongAnswer3 : Answer = new Answer();

  save() : void {
    if (this.question == null || this.question.text == null) {
      this.snackBar.open("Question text is mandatory.");
      return;
    }

    if (this.correctAnswer == null || this.correctAnswer.text == null) {
      this.snackBar.open("Correct answer is mandatory.");
      return;
    }
    
    if (this.wrongAnswer1 == null || this.wrongAnswer1.text == null ||
      this.wrongAnswer2 == null || this.wrongAnswer2.text == null ||
      this.wrongAnswer3 == null || this.wrongAnswer3.text == null) {

      this.snackBar.open("You need to inform three wrong answers.");
      return;
    }

    this.questionsService.save(this.question, this.correctAnswer, this.wrongAnswer1,
      this.wrongAnswer2, this.wrongAnswer3).subscribe(() => this.snackBar.open("Question successfully saved!"));

  }

}
