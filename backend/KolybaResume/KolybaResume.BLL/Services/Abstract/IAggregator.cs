using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.Services.Abstract;

public interface IAggregator
{
    Task<List<Vacancy>> Aggregate();
}