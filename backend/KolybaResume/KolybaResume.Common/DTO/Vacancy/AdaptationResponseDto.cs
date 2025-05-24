namespace KolybaResume.Common.DTO.Vacancy;

public class AdaptationResponseDto
{
    public int Score { get; set; }
    public string[] MissingKeywords { get; set; } = [];
}