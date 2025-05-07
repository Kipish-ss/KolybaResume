import { Observable, combineLatest, map, startWith } from 'rxjs';

import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
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

    filterControl = new FormControl('');
    remoteTypeControl = new FormControl('');
    sortControl = new FormControl('relevanceScore');

    public filteredResults$?: Observable<Vacancy[]>;

    constructor(private vacanciesStoreService: VacanciesStoreService) {

        this.vacanciesStoreService.loadVacancies();

        this.filteredResults$ = combineLatest([
            this.results$,
            this.filterControl.valueChanges.pipe(startWith('')),
            this.remoteTypeControl.valueChanges.pipe(startWith('')),
            this.sortControl.valueChanges.pipe(startWith('relevanceScore')),
        ]).pipe(
            map(([results, title, remoteType, sortKey]) =>
                results
                    ?.filter(r => r.title.toLowerCase().includes(title?.toLowerCase() ?? ''))
                    // .filter(r => (remoteType ? r.jobType === Number(remoteType) : true))
                    .sort((a, b) => (b[sortKey as keyof Vacancy] as number) - (a[sortKey as keyof Vacancy] as number)) ?? []
            )
        );
    }
}
