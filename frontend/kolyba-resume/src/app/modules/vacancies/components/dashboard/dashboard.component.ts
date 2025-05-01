import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { VacanciesStoreService } from '@vacancies//store/services/vacancies-store.service';

@Component({
    selector: 'kr-dashboard',
    standalone: false,
    templateUrl: './dashboard.component.html',
    styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
    public readonly hasResume$ = this.authStoreService.hasResume$;

    constructor(
        private readonly vacanciesStoreService: VacanciesStoreService,
        private readonly authStoreService: AuthStoreService,
        private readonly router: Router
    ) { }

    onSearchVacancies() {
        this.router.navigateByUrl('search-results');
    }

    onAdaptResume() {
        this.vacanciesStoreService.openVacancyInput();
    }
}
