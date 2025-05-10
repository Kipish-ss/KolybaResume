using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class VacancyUpdate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "CategoryText",
                table: "Vacancies",
                type: "text",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<int>(
                name: "Source",
                table: "Vacancies",
                type: "integer",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CategoryText",
                table: "Vacancies");

            migrationBuilder.DropColumn(
                name: "Source",
                table: "Vacancies");
        }
    }
}
