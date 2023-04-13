import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddQuestionComponent } from './components/add-question/add-question.component';
import { QuestionDetailsComponent } from './components/question-details/question-details.component';
import { QuestionListComponent } from './components/question-list/question-list.component';
import { AddCourseComponent } from './components/add-course/add-course.component';

const routes: Routes = [
  { path: '', redirectTo: 'questions', pathMatch: 'full' },
  { path: 'questions', component: QuestionListComponent },
  { path: 'questions/detail/:id', component: QuestionDetailsComponent },
  { path: 'questions/add', component: AddQuestionComponent },
  { path: 'courses', component: AddCourseComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
