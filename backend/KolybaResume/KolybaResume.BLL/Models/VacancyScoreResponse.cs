using System.Text.Json.Serialization;

namespace KolybaResume.BLL.Models;

public class VacancyScoreResponse
{
    [JsonPropertyName("vacancy_id")]
    public long VacancyId { get; set; }
    [JsonPropertyName("score")]
    public int Score { get; set; }
    [JsonPropertyName("user_id")]
    public long UserId { get; set; }
}