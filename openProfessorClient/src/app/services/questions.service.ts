import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, catchError } from 'rxjs';
import { Question } from '../models/question.model';
import { Answer } from '../models/answer.model';
import { Course } from '../models/course';

const baseUrl = 'http://localhost:8000/api';

@Injectable({
  providedIn: 'root'
})
export class QuestionsService {

  constructor(private httpClient : HttpClient) { }

  save(question : Question, correctAnswer : Answer, wrongAnswer1 : Answer,
    wrongAnswer2 : Answer, wrongAnswer3 : Answer) : Observable<any> {

      console.log('test');
      console.log(question.course);

    let data = {'question' : question.text, 
      'correct' : correctAnswer.text,
      'wrong1' : wrongAnswer1.text, 
      'wrong2' : wrongAnswer2.text, 
      'wrong3' : wrongAnswer3.text,
      'course_id' : question.course?.id};

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };

    return this.httpClient.post<any>(baseUrl + 'questions', data, httpOptions);
  }

  downloadMoodle(ids:string): any {
		return this.httpClient.get(`${baseUrl}/download-moodle/"${ids}"`, {responseType: 'blob'});
  }

  downloadLatex(ids:string): any {
		return this.httpClient.get(`${baseUrl}/download-latex/${ids}`, {responseType: 'blob'});
  }

  downloadAll(course: Course): any {
		return this.httpClient.get(`${baseUrl}/download-all/${course.id}`, {responseType: 'blob'});
  }
   
  getAll() : Observable<Question[]> {
    return this.httpClient.get<Question[]>(baseUrl + 'questions');
  }

  get(id : any) : Observable<Question> {
    return this.httpClient.get(`${baseUrl}/${id}`);
  }

  update(id : any, data : any) : Observable<any> {
    return this.httpClient.put(`${baseUrl}/${id}`, data);
  }

  delete(id : any) : Observable<any> {
    return this.httpClient.delete(`${baseUrl}/${id}`);
  }

  getIds(course : Course) : Observable<Number[]> {
    return this.httpClient.get<Number[]>(`${baseUrl}/questions/course/${course.id}`);
  }

}
