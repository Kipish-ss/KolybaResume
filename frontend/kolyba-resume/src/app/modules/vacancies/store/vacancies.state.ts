import { ResumeRecommendations } from "../models/resume-recommendations";
import { Vacancy } from "../models/vacancy";

export interface VacanciesState {
    searchResults?: Vacancy[];
    resumeRecommendations?: ResumeRecommendations;
    jobDescription?: string | null;
}

export function getVacanciesInitState(): VacanciesState {
    return { }
}