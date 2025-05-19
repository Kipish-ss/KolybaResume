using System.Text.Json.Serialization;

namespace KolybaResume.BLL.Models;

public class ResumeAdaptationRequest
{
    [JsonPropertyName("resume_id")]
    public long ResumeId { get; set; }
    [JsonPropertyName("vacancy_text")]
    public string VacancyText { get; set; } = string.Empty;
}