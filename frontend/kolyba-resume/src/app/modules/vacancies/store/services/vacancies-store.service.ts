import * as vacanciesActions from '../actions/vacancies.actions';
import * as vacanciesSelectors from '../selectors/vacancies.selector';

import { Injectable, inject } from '@angular/core';

import { Store } from '@ngrx/store';
import { User } from '@auth//models/user';

@Injectable({ providedIn: 'root' })
export class VacanciesStoreService {
    public searchResults$ = this.store.select(vacanciesSelectors.selectSearchResults);
    public resumeRecommendations$ = this.store.select(vacanciesSelectors.selectResumeRecommendations);
    public jobDescription$ = this.store.select(vacanciesSelectors.selectJobDescription);

    public constructor(private readonly store: Store) { }

    public openVacancyInput(): void {
        this.store.dispatch(vacanciesActions.openVacancyInputPopup());
    }

    public loadJobDescription(url: string): void {
        this.store.dispatch(vacanciesActions.loadJobDescription({ url }));
    }

    public loadVacancies(): void {
        this.store.dispatch(vacanciesActions.loadVacancies());
    }

    public loadRecommendations(jobDescription: string): void {
        this.store.dispatch(vacanciesActions.loadRecommendations({ jobDescription }));
    }

    public loadRecommendationsById(vacancyId: number): void {
        this.store.dispatch(vacanciesActions.loadRecommendationsById({ vacancyId }));
    }
}
