import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Course } from '../models/course';

const baseUrl = 'http://localhost:8000/api/courses';

@Injectable({
  providedIn: 'root'
})
export class CoursesService {

  constructor(private httpClient : HttpClient) { }

  save(course : Course) : Observable<any> {

    let data = {'name' : course.name};

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };

    return this.httpClient.post<any>(baseUrl, data, httpOptions);
  }

  getAll() : Observable<Course[]> {
    return this.httpClient.get<Course[]>(baseUrl);
  }

}
