using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddVacancyUrl : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Url",
                table: "Vacancies",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Url",
                table: "Vacancies");
        }
    }
}
