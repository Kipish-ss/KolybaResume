import { createFeatureSelector, createSelector } from "@ngrx/store";

import { VacanciesState } from "../vacancies.state";

export const selectVacanciesFeature = createFeatureSelector<VacanciesState>('vacancies');

export const selectSearchResults = createSelector(
    selectVacanciesFeature,
    state => state.searchResults
);

export const selectResumeRecommendations = createSelector(
    selectVacanciesFeature,
    state => state.resumeRecommendations
);

export const selectJobDescription = createSelector(
    selectVacanciesFeature,
    state => state.jobDescription
);