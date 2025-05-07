using KolybaResume.DAL.Context.Converters;
using KolybaResume.DAL.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace KolybaResume.DAL.Context.Configurations;

public class ResumeConfiguration : IEntityTypeConfiguration<Resume>
{
    public void Configure(EntityTypeBuilder<Resume> builder)
    {
        var vectorConverter = new ValueConverter<double[]?, byte[]?>(
            vector => vector == null ? null : VectorConverter.ToBytes(vector),
            bytes => bytes == null ? null : VectorConverter.FromBytes(bytes));

        builder.Property(e => e.Vector)
            .HasConversion(vectorConverter)
            .HasColumnType("bytea");
    }
}