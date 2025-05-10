export interface Vacancy {
    id: number;
    text: string;
    title: string;
    url: string;
    salary?: string;
    score: number;
    location?: string;
}