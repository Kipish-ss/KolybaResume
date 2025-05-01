import { Component } from '@angular/core';
import { VacanciesStoreService } from '@vacancies//store/services/vacancies-store.service';

@Component({
    selector: 'kr-resume-adaptation',
    standalone: false,
    templateUrl: './resume-adaptation.component.html',
    styleUrl: './resume-adaptation.component.scss'
})
export class ResumeAdaptationComponent {
    public readonly recommendation$ = this.vacanciesStoreService.resumeRecommendations$;

    constructor(private vacanciesStoreService: VacanciesStoreService) { }
}
