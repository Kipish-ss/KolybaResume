using KolybaResume.Common.Enums;

namespace KolybaResume.DAL.Entities;

public class Vacancy
{
    public long Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public double? SalaryMin { get; set; }
    public double? SalaryMax { get; set; }
    public JobType JobType { get; set; }
    public string? Location { get; set; }
    public double[]? Vector { get; set; }
    public JobCategory? Category { get; set; }
}