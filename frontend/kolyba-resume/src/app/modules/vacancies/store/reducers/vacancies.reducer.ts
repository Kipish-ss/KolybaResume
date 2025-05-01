import * as vacanciesActions from "../actions/vacancies.actions";

import { createReducer, on } from "@ngrx/store";

import { getVacanciesInitState } from "../vacancies.state";

export const vacanciesReducer = createReducer(
    getVacanciesInitState(),
    on(vacanciesActions.loadJobDescriptionSuccess, (state, action) => ({
        ...state,
        jobDescription: action.description
    })),
    on(vacanciesActions.loadRecommendationsSuccess, (state, action) => ({
        ...state,
        resumeRecommendations: action.recommendations
    })),
    on(vacanciesActions.loadVacanciesSuccess, (state, action) => ({
        ...state,
        searchResults: action.vacancies
    })),
    on(vacanciesActions.openVacancyInputPopup, (state) => ({
        ...state,
        jobDescription: null
    }))
);