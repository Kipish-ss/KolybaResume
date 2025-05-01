import { JobType } from "./job-type";

export interface Vacancy {
    id: number;
    text: string;
    title: string;
    salaryMin?: number;
    salaryMax?: number;
    jobType: JobType;
    score: number;
    location?: string;
}