using KolybaResume.Common.Enums;

namespace KolybaResume.DAL.Entities;

public class Vacancy
{
    public long Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string Salary { get; set; } = string.Empty;
    public string? Location { get; set; }
    public string CategoryText { get; set; } = string.Empty;
    public string CleanedText { get; set; } = string.Empty;
    public VacancySource Source { get; set; } = VacancySource.Dou;
    public double[]? Vector { get; set; }
    public JobCategory? Category { get; set; }
}