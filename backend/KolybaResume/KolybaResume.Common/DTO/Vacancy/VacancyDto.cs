using KolybaResume.Common.Enums;

namespace KolybaResume.Common.DTO.Vacancy;

public class VacancyDto
{
    public long Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public double? SalaryMin { get; set; }
    public double? SalaryMax { get; set; }
    public JobType JobType { get; set; }
    public string? Location { get; set; }
    public int Score { get; set; }
}