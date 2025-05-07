export interface Vacancy {
    id: number;
    text: string;
    title: string;
    link: string;
    salary?: string;
    score: number;
    location?: string;
}