import * as vacanciesActions from '../actions/vacancies.actions';

import { Observable, catchError, map, of } from 'rxjs';

import { Action } from '@ngrx/store';
import { HttpInternalService } from '@core/services/http-internal.service';
import { Injectable } from '@angular/core';
import { ResumeRecommendations } from '@vacancies//models/resume-recommendations';
import { Vacancy } from '@vacancies//models/vacancy';

@Injectable({
    providedIn: 'root',
})
export class VacanciesApiService {
    public routePrefix = '/vacancy';

    constructor(private httpService: HttpInternalService) {}

    public get(): Observable<Action> {
        return this.httpService.getRequest<Vacancy[]>(this.routePrefix).pipe(
            map((vacancies) => vacanciesActions.loadVacanciesSuccess({ vacancies })),
            catchError(() => of(vacanciesActions.loadVacanciesFailure({ error: new Error() }))),
        );
    }

    public getDescription(link: string): Observable<Action> {
        return this.httpService.postRequest<{ text: string}>(`${this.routePrefix}/description`, { link }).pipe(
            map((description) => vacanciesActions.loadJobDescriptionSuccess({ description: description.text })),
            catchError((error) => of(vacanciesActions.loadJobDescriptionFailure({ error: new Error() }))),
        );
    }

    public getRecommendations(jobDescription: string): Observable<Action> {
        return this.httpService.postRequest<ResumeRecommendations>(`${this.routePrefix}/recommendations`, { jobDescription }).pipe(
            map((recommendations) => vacanciesActions.loadRecommendationsSuccess({ recommendations })),
            catchError(() => of(vacanciesActions.loadRecommendationsFailure({ error: new Error() }))),
        );
    }
}
