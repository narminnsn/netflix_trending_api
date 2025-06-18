from typing import List, Literal, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from datetime import date
from app.models import Movie, Season, TVShow, ViewSummary


class CRUDTop10:

    def get_top10(
            self,
            db: Session,
            locale: str,
            window: Literal["WEEKLY", "SEMI_ANNUALLY"] = "WEEKLY",
            as_of: Optional[date] = None,
            include: Literal["movie", "season", "both"] = "both",
    ) -> List[dict]:
        """
        Returns the Top 10 titles (movie or season) for a given locale and time window.

        :param db: SQLAlchemy session
        :param locale: Market/language code (e.g., 'en', 'es')
        :param window: Reporting window, either WEEKLY or SEMI_ANNUALLY
        :param as_of: The reference date (defaults to latest available)
        :param include: 'movie', 'season', or 'both'
        :return: A list of up to 10 ranked titles
        """

        # 1. If as_of is not provided, get the latest date from the DB
        if not as_of:
            as_of = (
                db.query(ViewSummary.start_date)
                .filter(ViewSummary.duration == window)
                .order_by(ViewSummary.start_date.desc())
                .limit(1)
                .scalar()
            )
            if not as_of:
                return []

        # 2. Common filters
        filters = [
            ViewSummary.duration == window,
            ViewSummary.start_date <= as_of,
            ViewSummary.view_rank <= 10,
        ]

        response = []

        # 3. Movies
        if include in ("movie", "both"):
            movie_query = (
                db.query(
                    Movie.id.label("id"),
                    Movie.title.label("title"),
                    ViewSummary.view_rank,
                    ViewSummary.hours_viewed,
                    ViewSummary.views,
                    Movie.runtime,
                )
                .join(ViewSummary, ViewSummary.movie_id == Movie.id)
                .filter(*filters)
                .filter(Movie.locale == locale)
            )
            for row in movie_query.all():
                response.append({
                    "id": row.id,
                    "type": "movie",
                    "title": row.title,
                    "view_rank": row.view_rank,
                    "hours_viewed": row.hours_viewed,
                    "views": row.views,
                    "runtime": row.runtime,
                })

        # 4. Seasons — TVShow.title + " • S" + Season.season_number
        if include in ("season", "both"):
            season_title = func.concat_ws(" • S", TVShow.title, cast(Season.season_number, String)).label("title")

            season_query = (
                db.query(
                    Season.id.label("id"),
                    season_title,
                    ViewSummary.view_rank,
                    ViewSummary.hours_viewed,
                    ViewSummary.views,
                    Season.runtime,
                )
                .join(ViewSummary, ViewSummary.season_id == Season.id)
                .join(TVShow, TVShow.id == Season.tv_show_id)
                .filter(*filters)
                .filter(TVShow.locale == locale)
            )
            for row in season_query.all():
                response.append({
                    "id": row.id,
                    "type": "season",
                    "title": row.title,
                    "view_rank": row.view_rank,
                    "hours_viewed": row.hours_viewed,
                    "views": row.views,
                    "runtime": row.runtime,
                })

        # 5. Sort by view_rank and return top 10
        response.sort(key=lambda x: x["view_rank"])
        return response[:10]