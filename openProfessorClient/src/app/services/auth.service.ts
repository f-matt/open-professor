import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { JwtToken } from '../models/jwt-token';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
  
const baseUrl = "/api";

const TOKEN_NAME = "openProfessorToken";

@Injectable({
  providedIn: "root"
})
export class AuthService {

  private tokenSubject: BehaviorSubject<JwtToken | null>;

  constructor(
    private httpClient: HttpClient,
    private router: Router,
    private jwtHelperService: JwtHelperService) { 

    const tokenJson = localStorage.getItem(TOKEN_NAME);
    if (tokenJson) {
      let token = JSON.parse(tokenJson);
      this.tokenSubject = new BehaviorSubject(token);
    } else {
      this.tokenSubject = new BehaviorSubject<JwtToken | null>(null);
    }
  }

  public get tokenValue() {
    const token = this.tokenSubject.value;

    if (token && !this.jwtHelperService.isTokenExpired(token.access_token))
      return token.access_token;

    return null;
  }

  login(username: string, password: string) {
    return this.httpClient.post<JwtToken>(`${baseUrl}/login`, 
      {'username':username, 'password':password})
      .pipe(map(token => {
        localStorage.setItem(TOKEN_NAME, JSON.stringify(token));
        this.tokenSubject.next(token);
        return token;
      }));
  }

  refreshToken() {
    return this.httpClient.post<JwtToken>(`${baseUrl}/refresh`, 
      {})
      .pipe(map(token => {
        const existingTokenJson = localStorage.getItem(TOKEN_NAME);
        if (existingTokenJson) {
          let existingToken: JwtToken = JSON.parse(existingTokenJson);
          existingToken.access_token = token.access_token;
          localStorage.setItem(TOKEN_NAME, JSON.stringify(existingToken));
          this.tokenSubject.next(existingToken);
          return existingToken;
        }

        return null;
      }));
  }

  logout() {
    localStorage.removeItem(TOKEN_NAME);
    this.tokenSubject.next(null);
    this.router.navigate(['/login']);
  }

}
