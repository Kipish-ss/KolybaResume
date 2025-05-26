namespace KolybaResume.Common.DTO.Vacancy;

public class VacancyDto
{
    public long Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string Salary { get; set; } = string.Empty;
    public string? Location { get; set; }
    public int Score { get; set; }
}