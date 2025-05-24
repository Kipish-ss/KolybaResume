import { Observable, combineLatest, map, startWith } from 'rxjs';

import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { VacanciesStoreService } from '@vacancies//store/services/vacancies-store.service';
import { Vacancy } from '@vacancies//models/vacancy';

@Component({
    selector: 'kr-search-results',
    standalone: false,
    templateUrl: './search-results.component.html',
    styleUrl: './search-results.component.scss'
})
export class SearchResultsComponent {
    public readonly results$ = this.vacanciesStoreService.searchResults$;

    public readonly filterControl = new FormControl('');
    public readonly locationControl = new FormControl('');

    public filteredResults$?: Observable<Vacancy[]>;
    public locations$?: Observable<string[]>;

    constructor(
        private readonly vacanciesStoreService: VacanciesStoreService,
        private readonly authStoreService: AuthStoreService,
        private readonly router: Router
    ) {

        this.vacanciesStoreService.loadVacancies();

        this.filteredResults$ = combineLatest([
            this.results$,
            this.filterControl.valueChanges.pipe(startWith('')),
            this.locationControl.valueChanges.pipe(startWith(''))
        ]).pipe(
            map(([results, title, location]) =>
                results
                    ?.filter(r => r.title.toLowerCase().includes(title?.toLowerCase() ?? ''))
                    ?.filter(r => location === 'All' || r.location?.includes(location ?? '')) ?? []
            )
        );


        this.locations$ = this.results$.pipe(
            map(vacancies => [
                'All',
                ...(vacancies?.reduce((result, vacancy) => {
                    vacancy.location?.split(',').forEach(location => result.add(location.trim()));
                    return result;
                }, new Set<string>()) ?? [])
            ])
        )
    }

    public adaptResume(vacancyId: number): void {
        this.vacanciesStoreService.loadRecommendationsById(vacancyId);
    }

    public onSignOut(): void {
        this.authStoreService.signOut();
    }

    public goBack(): void {
        this.router.navigateByUrl('');
    }
}
