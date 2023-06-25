import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { JwtToken } from '../models/jwt-token';
import { Router } from '@angular/router';
  
const baseUrl = 'http://localhost:8000/api';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private tokenSubject: BehaviorSubject<JwtToken | null>;

  constructor(
    private httpClient: HttpClient,
    private router: Router) { 

    this.tokenSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('openProfessorToken')!));
  }

  public get tokenValue() {
    return this.tokenSubject.value;
  }

  login(username: string, password: string) {
    return this.httpClient.post<JwtToken>(`${baseUrl}/token/`, 
      {'username':username, 'password':password})
      .pipe(map(token => {
        localStorage.setItem('openProfessorToken', JSON.stringify(token));
        this.tokenSubject.next(token);
        return token;
      }));
  }

  refresh() {
    return this.httpClient.post<JwtToken>(`${baseUrl}/token/refresh`, 
      {})
      .pipe(map(token => {
        localStorage.setItem('openProfessorToken', JSON.stringify(token));
        this.tokenSubject.next(token);
        return token;
      }));
  }

  logout() {
    localStorage.removeItem('openProfesorToken');
    this.tokenSubject.next(null);
    this.router.navigate(['/login']);
  }

}
