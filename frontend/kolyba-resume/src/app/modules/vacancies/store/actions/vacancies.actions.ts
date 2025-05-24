import { createAction, props } from '@ngrx/store';

import { ResumeRecommendations } from '@vacancies//models/resume-recommendations';
import { Vacancy } from '../../models/vacancy';

export const openVacancyInputPopup = createAction('[Vacancies] Open vacancy input popup');

export const loadVacancies = createAction('[Vacancies] Load vacancies');
export const loadVacanciesSuccess = createAction('[Vacancies] Load vacancies success', props<{ vacancies: Vacancy[] }>());
export const loadVacanciesFailure = createAction('[Vacancies] Load vacancies failure', props<{ error: Error }>());

export const loadJobDescription = createAction('[Vacancies] Load job description', props<{ url: string }>());
export const loadJobDescriptionSuccess = createAction('[Vacancies] Load job description success', props<{ description: string }>());
export const loadJobDescriptionFailure = createAction('[Vacancies] Load job description failure', props<{ error: Error }>());

export const loadRecommendations = createAction('[Vacancies] Load recommendations', props<{ jobDescription: string }>());
export const loadRecommendationsById = createAction('[Vacancies] Load recommendations By Id', props<{ vacancyId: number }>());
export const loadRecommendationsSuccess = createAction('[Vacancies] Load recommendations Success', props<{ recommendations: ResumeRecommendations }>());
export const loadRecommendationsFailure = createAction('[Vacancies] Load recommendations Failure', props<{ error: Error }>());